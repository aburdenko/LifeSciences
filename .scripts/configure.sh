# Usage: source .scripts/configure.sh

# --- Gemini CLI Installation/Update ---
if ! command -v npm &> /dev/null; then
  echo "Error: npm is not installed. Please install Node.js and npm to continue." >&2
  return 1
fi

echo "Checking for the latest Gemini CLI version..."
LATEST_VERSION=$(npm view @google/gemini-cli version)

if ! command -v gemini &> /dev/null; then
  echo "Gemini CLI not found. Installing the latest version ($LATEST_VERSION)..."
  sudo npm install -g @google/gemini-cli@latest
else
  INSTALLED_VERSION=$(npm list -g @google/gemini-cli --depth=0 2>/dev/null | grep '@google/gemini-cli' | sed 's/.*@//')
  if [ "$INSTALLED_VERSION" == "$LATEST_VERSION" ]; then
    echo "Gemini CLI is already up to date (version $INSTALLED_VERSION)."
  else
    echo "A new version of Gemini CLI is available."
    echo "Upgrading from version $INSTALLED_VERSION to $LATEST_VERSION..."
    sudo npm install -g @google/gemini-cli@latest
  fi
fi

# --- uv Installation Check ---
if ! command -v uv &> /dev/null; then
  echo "uv not found. Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source $HOME/.local/bin/env
fi

# --- Environment Configuration ---
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Configuration file '$ENV_FILE' not found." >&2
    echo "Please create it by copying from '.env.example' and filling in the values." >&2
    return 1
fi

# Export .env variables
export $(grep -v '^#' "$ENV_FILE" | sed 's/#.*//' | xargs)

# --- Git User Configuration ---
if [ -n "$GIT_USER_NAME" ] && [ -n "$GIT_USER_EMAIL" ]; then
  echo "Configuring git user name and email..."
  git config --global user.name "$GIT_USER_NAME"
  git config --global user.email "$GIT_USER_EMAIL"
fi

# --- Google Credentials Setup ---
echo "--- Configuring Google Cloud Authentication & Project ---"

if [ -n "$SERVICE_ACCOUNT_KEY_FILE" ] && [ -f "$SERVICE_ACCOUNT_KEY_FILE" ]; then
  echo "Service Account key found at '$SERVICE_ACCOUNT_KEY_FILE'. Using it for authentication."
  export GOOGLE_APPLICATION_CREDENTIALS="$SERVICE_ACCOUNT_KEY_FILE"
  if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(jq -r .project_id "$SERVICE_ACCOUNT_KEY_FILE" 2>/dev/null)
    echo "Inferred PROJECT_ID from Service Account: $PROJECT_ID"
  fi
else
  echo "Falling back to gcloud Application Default Credentials."
  unset GOOGLE_APPLICATION_CREDENTIALS
  if ! gcloud auth application-default print-access-token &>/dev/null; then
    echo "User is not logged in for ADC. Running 'gcloud auth application-default login'..."
    gcloud auth application-default login --no-launch-browser --scopes=openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/cloud-platform
  fi

  if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
  fi
fi

if [ -n "$PROJECT_ID" ] && [ "$PROJECT_ID" != "(unset)" ]; then
  echo "Setting active gcloud project to: $PROJECT_ID"
  gcloud config set project "$PROJECT_ID"
fi

# --- uv Sync & Environment Setup ---
# Nesting the environment under .venv/python312 as requested
PYTHON_VERSION="3.12"
VENV_PATH=".venv/python${PYTHON_VERSION//./}"

if [ ! -d "$VENV_PATH" ]; then
  echo "Python virtual environment '$VENV_PATH' not found. Creating with uv..."
  # uv python install will download the latest distribution for the version if missing
  uv python install "$PYTHON_VERSION"
  # Create the virtual environment at the specific nested path
  uv venv "$VENV_PATH" --python "$PYTHON_VERSION"
fi

echo "Syncing dependencies with uv in $VENV_PATH..."
# Tell uv to use our specific nested environment path
export UV_PROJECT_ENVIRONMENT="$VENV_PATH"
uv sync --all-extras

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# --- System Dependencies ---
if ! command -v xvfb-run &> /dev/null; then
    echo "Installing system libraries for browser/UI tools (xvfb)..."
    sudo apt-get update && sudo apt-get install -y xvfb libxkbcommon0 libxkbcommon-x11-0 libgbm1 libasound2t64 unzip jq
fi

# --- VS Code Extension Setup ---
echo "Checking for 'emeraldwalk.runonsave' VS Code extension..."
CODE_OSS_EXEC="/opt/code-oss/bin/codeoss-cloudworkstations"
if [ -x "$CODE_OSS_EXEC" ] && ! $CODE_OSS_EXEC --list-extensions | grep -q "emeraldwalk.runonsave"; then
    echo "Installing 'emeraldwalk.runonsave'..."
    VSIX_URL="https://www.vsixhub.com/go.php?post_id=519&app_id=65a449f8-c656-4725-a000-afd74758c7e6&s=v5O4xJdDsfDYE&link=https%3A%2F%2Fmarketplace.visualstudio.com%2F_apis%2Fpublic%2Fgallery%2Fpublishers%2Femeraldwalk%2Fvsextensions%2FRunOnSave%2F0.3.2%2Fvspackage"
    curl -fail -L -A 'Mozilla/5.0' -o "/tmp/runonsave.vsix" "$VSIX_URL"
    $CODE_OSS_EXEC --install-extension "/tmp/runonsave.vsix"
    rm -f "/tmp/runonsave.vsix"
fi

# --- Playwright Dependencies ---
if uv pip show playwright &> /dev/null; then
  PLAYWRIGHT_MARKER=".venv/.playwright_deps_installed"
  if [ ! -f "$PLAYWRIGHT_MARKER" ]; then
      echo "Installing Playwright system dependencies..."
      uv run python -m playwright install-deps && touch "$PLAYWRIGHT_MARKER"
  fi
fi

# POSIX-compliant check for sourcing
if ! (return 0 2>/dev/null); then
  echo "ERROR: This script must be sourced."
  exit 1
fi

# --- ADK Web Server Function ---
adkweb() {
  if [ -z "$GCP_USER_ACCOUNT" ]; then
    echo "Error: GCP_USER_ACCOUNT is not set in your .env file." >&2
    return 1
  fi

  local current_user=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
  if [ "$current_user" != "$GCP_USER_ACCOUNT" ]; then
    echo "WARNING: Re-authenticating as '$GCP_USER_ACCOUNT'..."
    gcloud auth application-default login --project="$PROJECT_ID" --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/userinfo.email,openid" || return 1
  fi

  echo "Stopping any existing ADK web server on port 8001..."
  local pids=$(lsof -t -i :8001)
  [ -n "$pids" ] && kill $pids && sleep 2

  echo "Starting ADK web server..."
  # Use uv run adk web to start the server
  # We point it to api/agents directory. Note: each subdir should have __init__.py and agent.py
  nohup uv run adk web --port 8001 api/agents > output.log 2>&1 &
  echo "ADK web server started in background on port 8001. Check output.log for details."
}

export PATH=$PATH:$HOME/.local/bin:.scripts
alias gemini="gemini -y --model $GEMINI_MODEL_POWERFUL"

echo "Configuration complete. Environment is ready."

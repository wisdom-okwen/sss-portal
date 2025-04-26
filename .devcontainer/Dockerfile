# ────────────────────────────────────────────────────────────────────────────────
# Base image: Python 3.12 (Debian slim) – no more deadsnakes, no distutils issue
# ────────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive TZ=America/New_York
WORKDIR /workspace

# ────────────────────────────────────────────────────────────────────────────────
# System utilities
# ────────────────────────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        debian-keyring \
        debian-archive-keyring \
        git \
        gnupg \
        locales \
        postgresql-client \
        libpq-dev \
        build-essential \
        software-properties-common \
        sudo \
        tzdata \
        wget \
        zsh \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# ───── Caddy (stable, correct key + suite) ─────
RUN rm -f /etc/apt/sources.list.d/caddy*.list  && \
    curl -1sSf https://dl.cloudsmith.io/public/caddy/stable/gpg.key \
      | gpg --dearmor -o /usr/share/keyrings/caddy.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/caddy.gpg] \
         https://dl.cloudsmith.io/public/caddy/stable/deb/debian/ bookworm main" \
      | tee /etc/apt/sources.list.d/caddy.list && \
    apt-get update && apt-get install -y --no-install-recommends caddy && \
    rm -rf /var/lib/apt/lists/*


# ────────────────────────────────────────────────────────────────────────────────
# Node 22
# ────────────────────────────────────────────────────────────────────────────────
ENV NODE_MAJOR 22

RUN mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
    | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list \
 && apt-get update && apt-get install -y nodejs \
 && npm install -g npm@latest \
 && rm -rf /var/lib/apt/lists/*

# ────────────────────────────────────────────────────────────────────────────────
# Non-root vscode user
# ────────────────────────────────────────────────────────────────────────────────
ARG USERNAME=vscode USER_UID=1000 USER_GID=1000
RUN groupadd --gid $USER_GID $USERNAME \
 && useradd  --uid $USER_UID --gid $USER_GID -m $USERNAME -s /usr/bin/zsh \
 && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
 && chmod 0440 /etc/sudoers.d/$USERNAME

# Git defaults for VS Code
RUN git config --system core.editor "code --wait" \
 && git config --system safe.directory '/workspace'

# Node_modules volume placeholder
RUN mkdir -p /workspace/frontend/node_modules \
 && chown $USERNAME /workspace/frontend/node_modules
VOLUME /workspace/frontend/node_modules

# ────────────────────────────────────────────────────────────────────────────────
# zsh & Oh-My-Zsh cosmetics (as vscode user)
# ────────────────────────────────────────────────────────────────────────────────
USER $USERNAME
ENV HOME=/home/$USERNAME
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
 && sed -i 's/robbyrussell/kennethreitz/' ~/.zshrc \
 && echo 'source <(npm completion script)' >> ~/.zshrc \
 && echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.zshrc

# ────────────────────────────────────────────────────────────────────────────────
# OpenShift CLI (oc)
# ────────────────────────────────────────────────────────────────────────────────
RUN arch="$(arch)"; \
    case "$arch" in x86_64) TARGET='';; aarch64) TARGET='arm64-';; esac && \
    wget -qO /tmp/oc.tgz "https://github.com/okd-project/okd/releases/download/4.14.0-0.okd-2023-12-01-225814/openshift-client-linux-${TARGET}4.14.0-0.okd-2023-12-01-225814.tar.gz" \
 && tar -C /tmp -xzf /tmp/oc.tgz oc && sudo mv /tmp/oc /usr/bin/oc && rm -f /tmp/oc.tgz

# ────────────────────────────────────────────────────────────────────────────────
# Python dependencies
# ────────────────────────────────────────────────────────────────────────────────
COPY backend/requirements.txt /workspace/backend/requirements.txt
WORKDIR /workspace/backend
RUN pip install --no-cache-dir -r requirements.txt

# ────────────────────────────────────────────────────────────────────────────────
EXPOSE 1530 1531 1532

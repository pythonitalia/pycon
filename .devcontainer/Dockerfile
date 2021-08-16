FROM mcr.microsoft.com/vscode/devcontainers/universal:1-linux

SHELL ["/bin/bash", "-c"]

# Install asdf
RUN git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.8.1 && \
 echo ". $HOME/.asdf/asdf.sh" >> ~/.zshrc && \
 echo ". $HOME/.asdf/asdf.sh" >> ~/.bashrc

# Add asdf plugins

RUN . $HOME/.asdf/asdf.sh && \
    asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git && \
    asdf plugin-add python && \
    asdf plugin-add terraform https://github.com/asdf-community/asdf-hashicorp.git

RUN pip install poetry pre-commit

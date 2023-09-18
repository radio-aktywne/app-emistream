{
  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-unstable";
    };

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
    };
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      # Import local override if it exists
      imports = [
        (
          if builtins.pathExists ./local.nix
          then ./local.nix
          else {}
        )
      ];

      # Sensible defaults
      systems = [
        "x86_64-linux"
        "i686-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem = {
        config,
        pkgs,
        system,
        ...
      }: let
        node = pkgs.nodejs;
        python = pkgs.python311;
        nil = pkgs.nil;
        task = pkgs.go-task;
        trunk = pkgs.trunk-io;
        poetry = pkgs.poetry;
        cacert = pkgs.cacert;
        copier = pkgs.copier;
        ffmpeg = pkgs.ffmpeg;
        tini = pkgs.tini;
        su-exec = pkgs.su-exec;
        curlie = pkgs.curlie;
      in {
        # Override pkgs argument
        _module.args.pkgs = import inputs.nixpkgs {
          inherit system;
          config = {
            # Allow packages with non-free licenses
            allowUnfree = true;
            # Allow packages with broken dependencies
            allowBroken = true;
            # Allow packages with unsupported system
            allowUnsupportedSystem = true;
          };
        };

        # Set which formatter should be used
        formatter = pkgs.alejandra;

        # Define multiple development shells for different purposes
        devShells = {
          default = pkgs.mkShell {
            name = "dev";

            packages = [
              node
              python
              nil
              task
              trunk
              poetry
              cacert
              copier
              ffmpeg
              curlie
            ];

            shellHook = ''
              task install
              source .venv/bin/activate
            '';
          };

          package = pkgs.mkShell {
            name = "package";

            packages = [
              python
              task
              poetry
              cacert
            ];

            shellHook = ''
              task install
              source .venv/bin/activate
            '';
          };

          runtime = pkgs.mkShell {
            name = "runtime";

            packages = [
              python
              poetry
              cacert
              ffmpeg
              tini
              su-exec
            ];
          };

          template = pkgs.mkShell {
            name = "template";

            packages = [
              task
              copier
            ];
          };

          lint = pkgs.mkShell {
            name = "lint";

            packages = [
              node
              task
              trunk
            ];
          };

          test = pkgs.mkShell {
            name = "test";

            packages = [
              python
              task
              poetry
              cacert
              ffmpeg
            ];

            shellHook = ''
              task install
              source .venv/bin/activate
            '';
          };

          docs = pkgs.mkShell {
            name = "docs";

            packages = [
              node
              task
            ];
          };
        };
      };
    };
}

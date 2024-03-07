{
  description = "A Nix flake dev environment for Python dev";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShells = {
        default = pkgs.mkShell {



          packages = with pkgs; [


            (pkgs.python3.withPackages (python-pkgs: [
              python-pkgs.bleak
            ]))

            # Nix
            nil
            alejandra
          ];
        };
      };
    });
}

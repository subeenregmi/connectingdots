{
  description = "flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
  };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      stdenv = pkgs.stdenv;
      lib = pkgs.lib;
    in {
      devShells.${system}.default = pkgs.mkShell{
        name = "flake";

        NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
          stdenv.cc.cc
          pkgs.SDL2
          pkgs.zlib
          pkgs.glib # libgthread-2.0.so
        ];

        NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";

        packages = with pkgs; [
          python313
          poetry
          SDL2
        ];

        shellHook = ''
          export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH
          export LD_PRELOAD="${pkgs.SDL2}/lib/libSDL2.so"
        '';
      };
    };
}

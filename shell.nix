{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    gcc
    zlib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.zlib}/lib:${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH
  '';
}

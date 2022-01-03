{ pkgs }: {
    deps = [
        pkgs.python39
        pkgs.poetry
        pkgs.vim
        pkgs.nodePackages.prettier
    ];
}

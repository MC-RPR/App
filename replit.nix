{ pkgs }: {
    deps = [
        pkgs.python39Full
        pkgs.poetry
        pkgs.vim
        pkgs.nodePackages.prettier
    ];
}

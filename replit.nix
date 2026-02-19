{ pkgs }: {
  deps = [
	pkgs.python3
	pkgs.novnc
	pkgs.python3Packages.websockify
	pkgs.xvfb-run
	pkgs.xorg.xhost
  ];
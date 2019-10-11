.PHONY: test lockdeps

test:
	test/all

testvenv:
	test/all venv

lockdeps:
	make -C "base/{{cookiecutter.repo_name}}" lockdeps

updatesubmodules:
	git submodule update --remote

_default:
    @just --list

# run all notebooks as tests
test:
    uv run pytest --nbmake -n=auto

# start the myst book server (executes the notebooks so the outputs appear)
docs:
    uv run myst start --execute

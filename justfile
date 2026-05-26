sync:
    uvx poetry sync --no-root
    
update:
    uvx poetry update

clean:
    uvx pyclean . -d all

[working-directory: 'Software/Miniish']
miniish:
    uvx poetry run python -m miniish
    
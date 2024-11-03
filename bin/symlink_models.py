import os
from pathlib import Path

# Repo root assuming this script in in root/bin
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
models_dir = os.path.join(root_dir, "models")
apps = ["ComfyUI", "fluxgym"]
apps_model_paths = [os.path.join(root_dir, app, "models") for app in apps]


def symlink_files(src_dir: Path, target_dir: Path):
    if not src_dir.is_dir():
        print(f"Source directory '{src_dir}' does not exist or is not a directory.")
        return
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        print(f"Created target directory '{target_dir}'")

    # Iterate over all files in the source directory
    for item in src_dir.iterdir():
        if item.is_file():  # Only create symlinks for files, not directories
            # Define the symlink path in the target directory
            symlink_path = target_dir / item.name

            # Create the symbolic link
            try:
                symlink_path.symlink_to(item)
                print(f"Created symlink for '{item}' -> '{symlink_path}'")
            except FileExistsError:
                print(f"Symlink '{symlink_path}' already exists. Skipping.")
            except Exception as e:
                print(f"Error creating symlink for '{item}': {e}")


def symlink_models():
    for model_type_dir in Path(models_dir).iterdir():
        if model_type_dir.is_file():
            continue
        if model_type_dir.is_dir():
            for app_models in apps_model_paths:
                app_model_type_dir = Path(os.path.join(app_models, model_type_dir.name))
                symlink_files(model_type_dir, app_model_type_dir)


if __name__ == "__main__":
    symlink_models()

import os
import shutil
from pathlib import Path
import logging
import tempfile

logger = logging.getLogger(__name__)

def create_templates_directory(package_templates_dir: Path, templates_dir: Path, dry_run=False, force=False, skip_existing=False):
    """
    Create a 'templates' directory in the current working directory and populate it with template files
    from the package's templates directory.

    Args:
        package_templates_dir (Path): Path to the package's templates directory.
        templates_dir (Path): Path to the directory where templates will be copied.
        dry_run (bool): If True, show what changes would be made without making them.
        force (bool): If True, overwrite existing files without prompting.
        skip_existing (bool): If True, skip existing files without prompting or overwriting.

    Raises:
        FileNotFoundError: If the package templates directory is not found.
        PermissionError: If there's a permission issue creating directories or copying files.
        IOError: If there's an IO error during the copy process.
    """
    if not package_templates_dir.exists():
        logger.error(f"Package templates directory not found: {package_templates_dir}")
        raise FileNotFoundError(f"Package templates directory not found: {package_templates_dir}")

    if dry_run:
        logger.info("Dry run mode: No changes will be made.")

    try:
        if not dry_run:
            templates_dir.mkdir(exist_ok=True, parents=True)
            if not os.access(templates_dir, os.W_OK):
                raise PermissionError(f"No write permission for directory: {templates_dir}")
        logger.info(f"Templates directory {'would be' if dry_run else 'was'} created at: {templates_dir}")
    except PermissionError as e:
        logger.error(f"Permission error: {str(e)}")
        raise

    # Check available disk space only if not in dry run mode
    if not dry_run:
        try:
            _, _, free = shutil.disk_usage(templates_dir)
            required_space = sum(f.stat().st_size for f in package_templates_dir.glob('**/*') if f.is_file())
            if free < required_space:
                raise IOError(f"Insufficient disk space. Required: {required_space}, Available: {free}")
        except OSError as e:
            logger.error(f"Error checking disk space: {str(e)}")
            raise

    copied_files = []
    try:
        for template_file in package_templates_dir.iterdir():
            if template_file.is_file():
                dest_file = templates_dir / template_file.name
                if dest_file.exists():
                    if skip_existing:
                        logger.info(f"Skipping existing file: {dest_file}")
                        continue
                    if not force:
                        if dry_run:
                            logger.info(f"Would prompt to overwrite: {dest_file}")
                            continue
                        overwrite = input(f"{dest_file} already exists. Overwrite? (y/n): ").lower() == 'y'
                        if not overwrite:
                            logger.info(f"Skipping: {template_file.name}")
                            continue

                try:
                    if not dry_run:
                        # Use a temporary file to ensure atomic write
                        with tempfile.NamedTemporaryFile(dir=templates_dir, delete=False) as tmp_file:
                            shutil.copy2(template_file, tmp_file.name)
                            os.replace(tmp_file.name, dest_file)
                        copied_files.append(dest_file)
                    logger.info(f"Template {'would be' if dry_run else 'was'} copied: {template_file.name}")
                except (PermissionError, IOError) as e:
                    logger.error(f"Error copying {template_file.name}: {str(e)}")
                    raise

    except Exception as e:
        logger.error(f"An error occurred during the template creation process: {str(e)}")
        if not dry_run:
            # Clean up partially copied files
            for file in copied_files:
                file.unlink(missing_ok=True)
        raise

    logger.info("Template creation process completed.")

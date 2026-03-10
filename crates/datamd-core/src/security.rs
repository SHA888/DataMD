use crate::error::{Error, Result};
use std::path::{Path, PathBuf};

/// Resolve a path securely, preventing traversal outside the base directory.
pub fn resolve_secure_path<P: AsRef<Path>, B: AsRef<Path>>(file_path: P, base_dir: B) -> Result<PathBuf> {
    let base = base_dir.as_ref().canonicalize()?;

    // If absolute, use as-is; else join with base
    let target_raw = file_path.as_ref();
    let candidate = if target_raw.is_absolute() {
        target_raw.to_path_buf()
    } else {
        base.join(target_raw)
    };

    let target = candidate.canonicalize()?;
    if target.starts_with(&base) {
        Ok(target)
    } else {
        Err(Error::Security(format!(
            "path traversal detected: {}",
            target.display()
        )))
    }
}

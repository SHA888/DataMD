use crate::error::{Error, Result};
use serde::Deserialize;
use std::fs;
use std::path::Path;

#[derive(Debug, Deserialize, Default)]
pub struct Config {
    pub chunk_size: Option<usize>,
    pub allow_directory_traversal: Option<bool>,
}

impl Config {
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self> {
        let path_ref = path.as_ref();
        let content = fs::read_to_string(path_ref)?;
        let ext = path_ref
            .extension()
            .and_then(|e| e.to_str())
            .unwrap_or("");

        match ext {
            "toml" => toml::from_str(&content).map_err(Error::from),
            "json" | "" => serde_json::from_str(&content).map_err(Error::from),
            other => Err(Error::Config(format!("unsupported config extension: {other}"))),
        }
    }
}

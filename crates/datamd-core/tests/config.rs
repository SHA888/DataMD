use datamd_core::config::Config;
use tempfile::tempdir;
use std::fs;

#[test]
fn loads_json_config() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("config.json");
    fs::write(&path, r#"{"chunk_size": 123, "allow_directory_traversal": false}"#).unwrap();

    let cfg = Config::load(&path).unwrap();
    assert_eq!(cfg.chunk_size, Some(123));
    assert_eq!(cfg.allow_directory_traversal, Some(false));
}

#[test]
fn loads_toml_config() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("config.toml");
    fs::write(&path, "chunk_size = 456\nallow_directory_traversal = true").unwrap();

    let cfg = Config::load(&path).unwrap();
    assert_eq!(cfg.chunk_size, Some(456));
    assert_eq!(cfg.allow_directory_traversal, Some(true));
}

#[test]
fn errors_on_unsupported_extension() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("config.yaml");
    fs::write(&path, "chunk_size: 1").unwrap();

    let err = Config::load(&path).unwrap_err();
    assert!(err.to_string().contains("unsupported config extension"));
}

#[test]
fn errors_on_malformed_json() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("config.json");
    fs::write(&path, "{chunk_size:}").unwrap();

    let err = Config::load(&path).unwrap_err();
    assert!(err.to_string().contains("serde error"));
}

use datamd_core::security::resolve_secure_path;
use tempfile::tempdir;

#[test]
fn resolves_relative_path_inside_base() {
    let dir = tempdir().unwrap();
    let base = dir.path();
    let file_path = base.join("foo.txt");
    std::fs::write(&file_path, "data").unwrap();

    let resolved = resolve_secure_path("foo.txt", base).unwrap();
    assert_eq!(resolved, file_path.canonicalize().unwrap());
}

#[test]
fn rejects_absolute_path_outside_base() {
    let base_dir = tempdir().unwrap();
    let outside_dir = tempdir().unwrap();
    let outside_file = outside_dir.path().join("bar.txt");
    std::fs::write(&outside_file, "data").unwrap();

    let err = resolve_secure_path(&outside_file, base_dir.path()).unwrap_err();
    let msg = err.to_string();
    assert!(msg.contains("path traversal detected"));
}

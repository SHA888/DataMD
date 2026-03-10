use tracing_subscriber::{fmt, EnvFilter};

/// Initialize tracing subscriber with env filter (e.g., RUST_LOG=info)
pub fn init_logging(default_level: &str) {
    let env_filter = EnvFilter::try_from_default_env()
        .or_else(|_| EnvFilter::try_new(default_level))
        .unwrap_or_else(|_| EnvFilter::new("info"));

    fmt().with_env_filter(env_filter).init();
}

fn main() {
    eprintln!("TEST: Binary is running!");
    println!("TEST: This is stdout");
    std::thread::sleep(std::time::Duration::from_secs(2));
    eprintln!("TEST: About to exit");
}

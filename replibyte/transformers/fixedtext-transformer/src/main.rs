fn main() {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
    println!("{}", convert());
}

fn convert() -> &'static str {
    return "!";
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn convert_to_fixed_text() {
        assert_eq!(
            convert(),
            "!"
        )
    }
}

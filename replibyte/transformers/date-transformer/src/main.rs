use fake::faker::chrono::raw::DateTimeBefore;
use fake::locales::EN;
use fake::Fake;
use chrono::{DateTime, Utc, FixedOffset};

fn main() {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
    println!("{}", convert(input));
}

fn convert(input: String) -> String {
    return match input.len() {
        len if len == 0 => input,
        _ => DateTime::<FixedOffset>::parse_from_rfc3339(
            &DateTimeBefore(
                EN,
                DateTime::<FixedOffset>::parse_from_rfc3339("2000-01-01T16:39:57-00:00")
                    .unwrap()
                    .with_timezone(&Utc)
            ).fake::<String>(),
        ).unwrap().with_timezone(&Utc).date().to_string()
    };
}

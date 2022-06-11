use uuid::Uuid;
use rand::prelude::SliceRandom;
use sha2::{Sha256, Digest};

const ALLOWED_EMAILS: [&str; 2] = [
    "FAA3FD18C360B42CFD43C7C9BDD12F8696480480FD4AF25E80A9870B773DD965",
    "015D72CDCD11004F5A61323ACBB73DCE453566F2ACF6BBE141B57B975DB53213",
];

fn main() {
    let mut input = String::new();
    std::io::stdin().read_line(&mut input).unwrap();
    println!("{}", convert(input.trim().to_string()));
}

fn convert(input: String) -> String {
    return match input.len() {
        len if len == 0 => input,
        _ => {
            let mut hasher = Sha256::new();
            hasher.update(input.as_bytes());
            let result = hasher.finalize();
            let email_as_string = format!("{:X}", result);

            if ALLOWED_EMAILS.contains(&email_as_string.as_str()) {
                return input;
            }

            let domain = ["com", "net", "org", "pizza", "co.uk", "app"].choose(&mut rand::thread_rng()).unwrap();
            format!("{}@example.{}", Uuid::new_v4(), domain)
        }
    };
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn allowed_emails_are_not_transformed() {
        assert_eq!(
            convert("__fake__email@pycon.it".to_owned()),
            "__fake__email@pycon.it"
        )
    }

    #[test]
    fn any_other_not_allowed_email_is_transformed() {
        assert_ne!(
            convert("another@gmail.com".to_owned()),
            "another@gmail.com"
        )
    }
}

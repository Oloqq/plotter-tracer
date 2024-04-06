use getset::Getters;

#[derive(Debug, Getters, Clone, Copy)]
pub struct Bounds<T> {
    #[getset(get = "pub")]
    left: T,
    #[getset(get = "pub")]
    right: T,
    #[getset(get = "pub")]
    top: T,
    #[getset(get = "pub")]
    bottom: T,
}

impl<T> Bounds<T>
where
    T: PartialOrd,
{
    pub fn new(left: T, right: T, top: T, bottom: T) -> Self {
        assert!(left < right);
        assert!(top < bottom);
        Self {
            left,
            right,
            top,
            bottom,
        }
    }
}

from dataclasses import dataclass, field


@dataclass
class ThemeColors:
    primary: str = 'white'
    secondary: str = 'gray'
    font: str = 'black'


@dataclass
class ThemeFontSizes:
    small: int = 12
    medium: int = 16
    large: int = 24


@dataclass
class Theme:
    colors: ThemeColors = field(default_factory=ThemeColors)
    font_sizes: ThemeFontSizes = field(default_factory=ThemeFontSizes)


@dataclass
class ThemeManager:
    themes: dict[str, Theme] = field(default_factory=dict)
    default_theme: Theme = field(default_factory=Theme)
    __current_theme: Theme = field(default_factory=Theme)

    @property
    def theme(self) -> Theme:
        return self.__current_theme if self.__current_theme else self.default_theme

    def change_theme(self, theme_name: str):
        if theme_name in self.themes:
            self.__current_theme = self.themes[theme_name]
        else:
            raise ValueError(f'Theme "{theme_name}" not found in ThemeManager.')


font = ThemeFontSizes(small=10, medium=14, large=18)

DARK_THEME = Theme(
    colors=ThemeColors(primary='white', secondary='dark_gray', font='white'),
    font_sizes=font,
)


LIGHT_THEME = Theme(
    colors=ThemeColors(primary='black', secondary='light_gray', font='black'),
    font_sizes=font,
)

MANAGER = ThemeManager(
    themes={
        'dark': DARK_THEME,
        'light': LIGHT_THEME,
    },
    default_theme=DARK_THEME,
)

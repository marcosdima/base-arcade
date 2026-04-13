class Functions:
    @classmethod
    def get_dict_keys(cls, d: dict, parent_key: str = "", separator: str = ".") -> list[str]:
        '''Return a sorted list of all keys in the given dictionary, including nested keys.'''
        keys = set()

        for key, value in d.items():
            full_key = f"{parent_key}{separator}{key}" if parent_key else key
            keys.add(full_key)
            if isinstance(value, dict):
                nested_keys = cls.get_dict_keys(value, full_key, separator)
                keys.update(nested_keys)
        
        return sorted(keys)
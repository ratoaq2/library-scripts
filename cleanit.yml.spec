templates:
  common:
    type: text
    match: contains

groups:
  blacklist:
    template: common
    rules:
      - Portuguese - Brazilian
      - Portuguese - BR
      - \bs\d{2}\s?e\d{2}\b: {type: regex, flags: ignorecase}
      - \b\d{2}x\d{2}\b: {type: regex}

  tidy:
    template: common
    type: regex
    match: contains
    rules:
      # Description: Replace extra spaces to a single space
      # Example:
      #   Foo     bar.
      # to
      #   Foo bar.
      - '\s{2,}': ' '

      # Description: Replace double single-quotes by double-quotes
      # Example:
      #   ''FooBar''
      # to
      #   "FooBar"
      - '\''{2,}': '"'

      # Description: Removes unneeded extra spaces at the end of a phrase before punctuation
      # Example:
      #   "FooBar" ...
      # to
      #   "FooBar"...
      - '(\S)\s+(\.{1,3})$': '\1\2'

      # Description: Add space when starting phrase with '-'. It ignores tags, such as <i>, <b>
      # Example:
      #   <i>-Francine, what has happened?
      #   -What has happened? You tell me!</i>
      # to
      #   <i>- Francine, what has happened?
      #   - What has happened? You tell me!</i>
      - '(?:^(|(?:\<\w\>)))-((?:\.{2,3})?[''"]?\w+)': { replacement: '\1- \2', flags: [multiline, unicode] }

      - ((Ah+)|(Oh+)|(Hu+m+))\W?: {match: exact}
      - .: {type: text, match: exact}
      - ^\s*$: {match: exact}


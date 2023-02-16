module.exports = {
    extends: [
      "eslint:recommended",
      "plugin:@typescript-eslint/recommended",
      "plugin:@typescript-eslint/recommended-requiring-type-checking",
    ],
    plugins: ["@typescript-eslint"],
    parser: "@typescript-eslint/parser",
    parserOptions: {
      project: true,
      tsconfigRootDir: __dirname,
    },
    root: true,
    rules: {
        "@typescript-eslint/semi": ["error", "always"],
        "@typescript-eslint/quotes": ["error", "double"],
        "@typescript-eslint/indent": ["error", 2],
    }
};
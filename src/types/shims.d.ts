declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.css';

interface ImportMetaEnv {
  [key: string]: any;
}

interface ImportMeta {
  env: ImportMetaEnv;
}

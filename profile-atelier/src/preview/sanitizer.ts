import DOMPurify from "dompurify";

const ALLOWED_TAGS = [
  "a",
  "b",
  "blockquote",
  "br",
  "code",
  "dd",
  "del",
  "details",
  "div",
  "dl",
  "dt",
  "em",
  "h1",
  "h2",
  "h3",
  "h4",
  "h5",
  "h6",
  "hr",
  "i",
  "img",
  "input",
  "ins",
  "kbd",
  "li",
  "ol",
  "p",
  "picture",
  "pre",
  "q",
  "rp",
  "rt",
  "ruby",
  "s",
  "samp",
  "source",
  "span",
  "strike",
  "strong",
  "sub",
  "summary",
  "sup",
  "table",
  "tbody",
  "td",
  "tfoot",
  "th",
  "thead",
  "tr",
  "tt",
  "ul",
  "var",
];

const ALLOWED_ATTR = [
  "align",
  "alt",
  "aria-hidden",
  "checked",
  "class",
  "disabled",
  "height",
  "href",
  "id",
  "loading",
  "media",
  "name",
  "open",
  "rel",
  "sizes",
  "src",
  "srcset",
  "style",
  "target",
  "title",
  "type",
  "valign",
  "width",
];

export function sanitizeHtml(rawHtml: string): string {
  if (!rawHtml) return "";

  const purifier =
    typeof (DOMPurify as any) === "function" && typeof window !== "undefined"
      ? (DOMPurify as any)(window)
      : (DOMPurify as any).default || DOMPurify;

  if (!purifier || typeof purifier.sanitize !== "function") {
    return rawHtml;
  }

  return purifier.sanitize(rawHtml, {
    ALLOWED_TAGS,
    ALLOWED_ATTR,
    ADD_TAGS: ["picture", "source", "details", "summary"],
    ADD_ATTR: ["media", "srcset", "target", "rel", "open", "align", "width", "height", "style"],
    ADD_DATA_URI_TAGS: ["img", "source"],
    ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto|tel|callto|blob|data):|[^a-z]|[a-z+.-]+(?:[^a-z+.-:]|$))/i,
    FORCE_BODY: false,
  });
}

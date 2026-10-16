/**
 * Safely resolves nested property paths such as "user.name" or "projects[0].title".
 */
export function getNestedValue(obj: any, path: string): any {
  if (!obj || typeof obj !== "object") return undefined;

  // Direct lookup first (e.g. key containing dots or special characters)
  if (path in obj) {
    return obj[path];
  }

  // Normalize array access e.g. "items[0].name" -> "items.0.name"
  const normalized = path.replace(/\[(\d+)\]/g, ".$1").trim();
  const segments = normalized.split(".");

  let current = obj;
  for (const segment of segments) {
    if (current == null) return undefined;
    current = current[segment];
  }

  return current;
}

/**
 * Replaces placeholder variables in markdown content.
 * Supports {{variable}}, {{ variable }}, ${variable}, and ${ variable }.
 * Supports nested paths like {{projects.0.title}}.
 */
export function substituteVariables(
  content: string,
  variables: Record<string, any> = {}
): string {
  if (!content || !variables || Object.keys(variables).length === 0) {
    return content;
  }

  // Replace {{ key }} patterns
  let result = content.replace(/\{\{\s*([\w.[\]-]+)\s*\}\}/g, (match, key) => {
    const val = getNestedValue(variables, key);
    if (val !== undefined && val !== null) {
      return typeof val === "object" ? JSON.stringify(val) : String(val);
    }
    return match;
  });

  // Replace ${ key } patterns
  result = result.replace(/\$\{\s*([\w.[\]-]+)\s*\}/g, (match, key) => {
    const val = getNestedValue(variables, key);
    if (val !== undefined && val !== null) {
      return typeof val === "object" ? JSON.stringify(val) : String(val);
    }
    return match;
  });

  return result;
}


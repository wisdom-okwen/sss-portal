export async function login(email, password) {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  if (response.ok && data.access_token) {
    localStorage.setItem("access_token", data.access_token);
    return { success: true, user: data.user };
  } else {
    return { success: false, error: data.detail || "Login failed" };
  }
}

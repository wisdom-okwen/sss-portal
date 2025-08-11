export async function login(email, password) {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  let data;
  try {
    data = await response.json();
  } catch (e) {
    return { success: false, error: "Invalid server response" };
  }
  if (response.ok && data.access_token && isValidJWT(data.access_token)) {
    localStorage.setItem("access_token", data.access_token);
    return { success: true, user: data.user };
  } else {
    return { success: false, error: data.detail || "Login failed" };
  }
}

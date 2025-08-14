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
  if (response.ok && data.access_token) {
    localStorage.setItem("access_token", data.access_token);
    return { success: true, user: data.user };
  } else {
    return { success: false, error: data.detail || "Login failed" };
  }
}

export async function getUser() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    return null;
  }
  const response = await fetch("/api/auth/me", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    return null;
  }
  try {
    const data = await response.json();
    return data.user || data;
  } catch (e) {
    return null;
  }
}

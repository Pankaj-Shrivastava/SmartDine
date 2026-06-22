// In production (Vercel), VITE_API_URL is set to the Railway backend URL at build time.
// Locally, it is unset so we fall back to the relative path served via Vite's dev proxy.
const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "/api/v1";

export async function fetchRecommendations(formData) {
    try {
        const response = await fetch(`${API_BASE}/recommend`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });

        if (response.ok) {
            const data = await response.json();
            return {
                success: true,
                recommendations: data.recommendations,
                metadata: data.query_metadata,
            };
        }

        if (response.status === 404) {
            return {
                success: false,
                errorType: "not_found",
                message: "No restaurants found. Try a different location or broader filters.",
            };
        }

        if (response.status === 422) {
            return {
                success: false,
                errorType: "validation",
                message: "Invalid search parameters. Please check your inputs.",
            };
        }

        return {
            success: false,
            errorType: "server",
            message: `Server error (${response.status}). Please try again.`,
        };
    } catch (error) {
        return {
            success: false,
            errorType: "connection",
            message: "Cannot connect to the backend. Ensure FastAPI is running on port 8000.",
        };
    }
}

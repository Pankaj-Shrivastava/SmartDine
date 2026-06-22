import { useState, useCallback } from "react";
import { fetchRecommendations } from "../api/client";

export function useRecommendations() {
    const [results, setResults] = useState(null);
    const [metadata, setMetadata] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const search = useCallback(async (formData) => {
        setIsLoading(true);
        setError(null);

        const result = await fetchRecommendations(formData);

        if (result.success) {
            setResults(result.recommendations);
            setMetadata(result.metadata);
        } else {
            setResults(null);
            setMetadata(null);
            setError({ type: result.errorType, message: result.message });
        }

        setIsLoading(false);
    }, []);

    const clearResults = useCallback(() => {
        setResults(null);
        setMetadata(null);
        setError(null);
    }, []);

    return { results, metadata, isLoading, error, search, clearResults };
}

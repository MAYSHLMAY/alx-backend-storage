-- Lists all bands with Glam Rock as their main style, ranked by their longevity
SELECT 
    band_name, 
    IFNULL(split, 2022) - IFNULL(formed, 0) AS lifespan
FROM 
    metal_bands
WHERE 
    style LIKE '%Glam Rock%'
ORDER BY 
    lifespan DESC;

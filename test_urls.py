#!/usr/bin/env python
"""
Script para probar que todas las URLs funcionan correctamente
"""
import requests
import sys

def test_urls():
    base_url = "http://127.0.0.1:8000"
    
    urls_to_test = [
        "/",
        "/dashboard/",
        "/zona-pruebas/",
        "/proceso-entrenamiento/",
        "/detalles-uso/",
        "/login/",
        "/signup/",
    ]
    
    print("🧪 Probando URLs...")
    print("=" * 50)
    
    for url in urls_to_test:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            status = "✅ OK" if response.status_code == 200 else f"❌ Error {response.status_code}"
            print(f"{url:<25} - {status}")
        except requests.exceptions.RequestException as e:
            print(f"{url:<25} - ❌ Error: {str(e)}")
    
    print("=" * 50)
    print("✅ Prueba completada")

if __name__ == "__main__":
    test_urls()

# CC3S2-PC3
PC3 del curso CC23S2 Desarrollo de Software. Se desarrolló el proyecto 6 - DevSecOps local: Escaneo SAST e IaC Security Checks.

## Requerimientos

- Python 3.x
- Instalar mediante `pipx` (recomendado para instalar aplicaciones de Python)
   - `bandit`
   - `checkov`
- `tflint`
- `shellcheck`
- Terraform
- Cron (Cualquier implementación)

## Utilidades

### Scripts

Todos los resultados de los scripts son almacenados en el directorio `reports/` en formato JSON.

- **scan_bandit.sh**: Ejecuta `bandit` para análisis estático de seguridad sobre los scripts de Python en el directorio `src/`.
- **scan_checkov.sh**: Ejecuta `checkov` para análisis de configuraciones de Terraform en el directorio `iac/`.
- **scan_shellcheck.sh**: Ejecuta `shellcheck` para análisis de scripts de shell en `scripts/`.
- **scan_tflint.sh**: Ejecuta `tflint` sobre los módulos de Terraform en el directorio `iac/`.
- **run_all_scans.sh**: Ejecuta todos los scripts de escaneo (`scan_bandit.sh`, `scan_checkov.sh`, `scan_shellcheck.sh`, `scan_tflint.sh`) y genera el reporte final con `security_checker.py`.
- **serve_reports.sh**: Lee el reporte generado por `security_checker.py` y lo sirve en un servidor Python en el navegador.


### Source
- **security_checker.py**: Revisa todos los reportes, genera un archivo markdown y un html con las vulnerabilidades encontradas.
- **schedule_scan.py**: Ejecuta los scans llamando a `scripts/run_all_scans.sh` y compara la cantidad de errores encontrados en el reporte generado con el reporte anterior de reports. Incluye instrucciones simples para ejecutar el script con `cron` periódicamente.

#### cron

Para programar la ejecución de `schedule_scan.py` periódicamente, se necesita alguna implementación de `cron` instalada en el sistema Linux del usuario. Con `cron` instalado, se debe activar el daemon:

```bash
$ sudo systemctl enable <implementacion de cron>.service
$ sudo systemctl start <implementacion de cron>.service
```

Una vez activado, se agrega una entrada para programar la ejecución de `schedule_scan.py`:

```bash
$ crontab -e
```

En el editor que se muestra, agregar una entrada como la siguiente:

```
0 9 * * * <ruta absoluta a schedule_scan.py>
```

### Utils

- **prettify_json.py**: Aplica un formato legible a los archivos JSON generados.
- **plot_generator.py**: Genera un gráfico de tarta/pie de los archivos JSON generados en el directorio `reports/`.

### Templates
- **security_report_template.html**: Plantilla usada para generar el dashboard html con la información de todo lo hallado.

### Utils

- **prettify_json.py**: Aplica un formato legible a los archivos JSON generados.
- **plot_generator.py**: Genera un gráfico de tarta/pie de los archivos JSON generados en el directorio `reports/`.
## Indicaciones para los desarrolladores

### Issues

El formato a utilizar para la escritura de issues se encuentra `.github/ISSUE_TEMPLATE/user_story.md`, el cual se creará automáticamente al crear issues a través de GitHub. Este formato está basado en el desarrollo basado en comportamientos (BDD por sus siglas en inglés) y es el propuesto para las actividades 18 y 19 del curso.

### Git Hooks

Los hooks a usar se encuentran en el directorio `.githooks`. Para activarlos, sigue las siguientes instrucciones:

#### Activación de hooks

##### Requerimientos

1. Instalar mediante `pipx` (recomendable para instalar aplicaciones Python):
   - black
   - flake8
   - pytest
2. Terraform
3. Shellcheck

#### ¿Cómo activarlo?

En el repositorio, ejecutar:

```bash
git config core.hooksPath .githooks
```

Además, se debe asegurar de que sean ejecutables:

```bash
chmod +x .githooks/*
```

#### En caso no se quiera usar pipx

Se pueden modificar los hooks para usar black, flake8 y pytest como aplicaciones en un entorno virtual en lugar de instalar como aplicaciones globalmente utilizando `pipx`.

1. En un entorno virtual, instalar los requerimientos como cualquier librería.
2. Modificar los scripts en los que se usen estas herramientas para que empiecen con `python -m <herramienta>`.

### Hooks utilizados

1. **commit-msg**: Verifica que los mensajes sigan recomendaciones de [commits convencionales](https://www.conventionalcommits.org/en/v1.0.0/).
2. **pre-commit**: Verifica que el código Python sea formateado y verificado por Black y Flake8. De igual modo, los archivos .tf son verificados con `terraform validate` y `terraform fmt -check`.
3. **pre-push**: Ejecuta el suite de tests para Python en Pytest.

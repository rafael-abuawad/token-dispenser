# 🪙 Token Dispenser

Un dispensador inteligente de tokens ERC-20 construido con Solidity y Ape Framework. Este proyecto permite a los usuarios crear sus propios tokens personalizados de manera fácil y rápida.

## 📋 Descripción

El **Token Dispenser** es un contrato inteligente que facilita la creación de tokens ERC-20 personalizados. Los usuarios pueden crear tokens con nombres y símbolos únicos pagando una pequeña tarifa de 0.1 ETH.

### Características Principales

- ✅ **Creación rápida de tokens**: Crea tokens ERC-20 con un solo clic
- ✅ **Tarifa fija**: Solo 0.1 ETH por token creado
- ✅ **Tokens completos**: Cada token incluye funcionalidades ERC-20 estándar
- ✅ **Propiedad clara**: El creador del token es automáticamente el propietario
- ✅ **Funcionalidades avanzadas**: Los tokens incluyen burning, permit y ownership

## 🏗️ Arquitectura

### Contratos

#### `TokenDispenser.sol`
- Contrato principal que maneja la creación de tokens
- Cobra una tarifa fija de 0.1 ETH por cada token creado
- Mantiene un registro de todos los tokens creados
- Asigna la propiedad del token al creador

#### `Token.sol`
- Contrato de token ERC-20 estándar
- Extiende OpenZeppelin con funcionalidades adicionales:
  - **ERC20Burnable**: Permite quemar tokens
  - **ERC20Permit**: Permite aprobaciones sin transacciones
  - **Ownable**: Control de propiedad del token

## 🚀 Instalación

### Prerrequisitos

- Python 3.13 o superior
- Node.js (para dependencias de Solidity)
- Una wallet con ETH para testing

### Configuración

1. **Clona el repositorio**
```bash
git clone <tu-repositorio>
cd token-dispenser
```

2. **Instala las dependencias**
```bash
# Instala uv si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instala las dependencias del proyecto
uv sync

# Instala los plguins de Apeworx
uv run ape plugins install .
```

3. **Configura tu cuenta**
```bash
# Crea una cuenta para testing
ape accounts generate brave
```

## 🧪 Testing

Ejecuta los tests para verificar que todo funciona correctamente:

```bash
# Ejecuta todos los tests
ape test

# Ejecuta tests específicos
ape test tests/test_dispenser.py
ape test tests/test_token.py
```

### Tests Incluidos

- ✅ Verificación de tarifa correcta (0.1 ETH)
- ✅ Creación exitosa de tokens
- ✅ Validación de tarifa insuficiente
- ✅ Creación de múltiples tokens
- ✅ Propiedades del contrato de token
- ✅ Longitud del array de tokens

## 🚀 Despliegue

### Despliegue Local (Anvil)

```bash
# Inicia Anvil en una terminal
anvil

# En otra terminal, despliega el contrato
ape run scripts/deploy.py
```

### Despliegue en Red Pública

```bash
# Configura tu cuenta con fondos
ape accounts load brave

# Despliega en la red deseada
ape run scripts/deploy.py --network ethereum:mainnet
```

## 📖 Uso

### Crear un Token

```python
from ape import project, accounts

# Carga tu cuenta
cuenta = accounts.load("brave")

# Despliega el dispensador (solo una vez)
dispensador = project.TokenDispenser.deploy(sender=cuenta, publish=True)

# Crea un nuevo token
nombre = "Mi Token"
simbolo = "MTK"
tarifa = dispensador.fee()

# Ejecuta la transacción
tx = dispensador.mint(nombre, simbolo, sender=cuenta, value=tarifa)

# Obtén la dirección del token creado
token_address = dispensador.tokens(0)  # Primer token
token = project.Token.at(token_address)

print(f"Token creado: {token_address}")
print(f"Nombre: {token.name()}")
print(f"Símbolo: {token.symbol()}")
print(f"Propietario: {token.owner()}")
```

### Interactuar con el Token

```python
# Acuñar tokens (solo el propietario)
token.mint(cuenta, 1000 * 10**18, sender=cuenta)

# Transferir tokens
token.transfer(otra_cuenta, 100 * 10**18, sender=cuenta)

# Quemar tokens
token.burn(50 * 10**18, sender=cuenta)
```

## 🔧 Scripts Disponibles

### `scripts/deploy.py`
Despliega el contrato TokenDispenser en la red especificada.

### `scripts/verify.py`
Verifica el contrato en el explorador de bloques.

## 📊 Funcionalidades del Token

Cada token creado incluye:

- **Transferencias estándar**: `transfer()`, `transferFrom()`
- **Aprobaciones**: `approve()`, `allowance()`
- **Quemado**: `burn()`, `burnFrom()`
- **Permit**: Aprobaciones sin transacciones
- **Acuñación**: Solo el propietario puede acuñar nuevos tokens
- **Propiedad**: Control total del token por el creador

## 🔒 Seguridad

- ✅ Tarifa fija y predecible
- ✅ Propiedad clara del token
- ✅ Validaciones de entrada
- ✅ Uso de OpenZeppelin (auditado)
- ✅ Tests exhaustivos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa los tests para ejemplos de uso
2. Verifica que tienes la versión correcta de Python (3.13+)
3. Asegúrate de que tu cuenta tiene fondos suficientes
4. Abre un issue en el repositorio

---

**¡Disfruta creando tus tokens! 🚀**
# Environment Variables

| Environment Name | Description                                      |
| ---------------- | ------------------------------------------------ |
| `JWT_SECRET_KEY` | Contains the Private Key (EdDSA) for JWT Signing |
| `JWT_PUBLIC_KEY` | For verifying the JWT keys (It also uses EdDSA)  |

# Generating EdDSA Key

- Open Terminal and then enter the following command to generate Ed25519 Key

  ```sh
  openssl genpkey -algorithm ed25519 -out jwt.pem
  ```

- Now for extracting public key from private key use

  ```sh
  openssl pkey -in jwt.pem -pubout -out jwt_public.pem
  ```

- Now `jwt.pem` contains the EdDSA Private Key and `jwt_public.pem` contains teh EdDSA Public Key

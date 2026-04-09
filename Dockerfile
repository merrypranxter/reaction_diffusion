# Multi-stage build for chemical-diffusion-reactions

# Build stage
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    gfortran \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml setup.py ./
COPY cpu/fortran_backend.f90 ./cpu/

RUN pip install --no-cache-dir numpy Cython scipy

# Build extensions
COPY cpu/cython_accelerated.pyx ./cpu/
RUN python setup.py build_ext --inplace

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgfortran5 \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Copy built extensions and source
COPY --from=builder /build/*.so ./cpu/
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Install package
COPY . .
RUN pip install --no-cache-dir -e ".[all]"

# Expose port for Jupyter
EXPOSE 8888

# Default: run parameter scan
ENTRYPOINT ["python", "-m", "tools.parameter_scanner"]
CMD ["--help"]

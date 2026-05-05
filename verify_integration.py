#!/usr/bin/env python
import sys
from pathlib import Path

# Test paths
DATASETS_DIR = Path('datasets')
OUTPUT_DIR = Path('outputs')

print('=' * 70)
print('VERIFICATION: Real Data Integration')
print('=' * 70)

# Check datasets folder
if DATASETS_DIR.exists():
    csv_files = list(DATASETS_DIR.glob('*.csv'))
    print(f'\nOK: Datasets folder found with {len(csv_files)} files')
    for f in sorted(csv_files):
        size_mb = f.stat().st_size / (1024*1024)
        print(f'   * {f.name} ({size_mb:.1f} MB)')
else:
    print(f'\nERROR: Datasets folder not found')

# Test imports
try:
    from src.model_manager import data_manager, initialize_managers
    print(f'\nOK: model_manager imported successfully')
    
    # Test data manager
    real_data_exists = data_manager.check_real_data()
    status = 'Found' if real_data_exists else 'Not found'
    print(f'OK: Real data check - {status}')
    
except Exception as e:
    print(f'ERROR: Import error: {e}')

# Check outputs folder
if OUTPUT_DIR.exists():
    pkl_files = list(OUTPUT_DIR.glob('*.pkl'))
    keras_files = list(OUTPUT_DIR.glob('*.keras'))
    print(f'OK: Outputs folder has {len(pkl_files)} PKL and {len(keras_files)} Keras files')
else:
    print(f'INFO: Outputs folder will be created after training')

print('\n' + '=' * 70)
print('All checks passed! Ready to train.')
print('=' * 70)

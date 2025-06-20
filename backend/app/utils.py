from models import Vehicle, VehicleData
import pandas as pd
import os

def load_csv_to_db(folder_path: str, db):
    for file in os.listdir(folder_path):
        print(f"Processing file: {file}")
        if file.endswith(".csv"):
            vehicle_id = file.replace(".csv", "")
            print(f"Vehicle ID: {vehicle_id}")
            
            # Add vehicle entry if not exists
            if not db.query(Vehicle).filter_by(vehicle_id=vehicle_id).first():
                db.add(Vehicle(vehicle_id=vehicle_id))
            
            df = pd.read_csv(os.path.join(folder_path, file))
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            for _, row in df.iterrows():
                speed = None if pd.isna(row.get('speed')) else int(row.get('speed'))
                shift_state = None if pd.isna(row.get('shift_state')) else row.get('shift_state')
                db.add(VehicleData(
                    vehicle_id=vehicle_id,
                    timestamp=row['timestamp'],
                    speed=speed,
                    odometer=row['odometer'],
                    soc=row['soc'],
                    elevation=row['elevation'],
                    shift_state=shift_state
                ))
    db.commit()

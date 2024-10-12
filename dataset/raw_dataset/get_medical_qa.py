from datasets import load_dataset

iCliniq_ds = load_dataset("lavita/ChatDoctor-iCliniq")
## save in csv
iCliniq_ds.save_to_disk("iCliniq_data_hf_dataset")

health_care_magic_ds = load_dataset("lavita/ChatDoctor-HealthCareMagic-100k")
health_care_magic_ds.save_to_disk("health_care_magic_hf_dataset")

if __name__ == "__main__":
    for i in range(10):
        print(iCliniq_ds)
        print(iCliniq_ds["train"][i])
        print("=========")
        print(health_care_magic_ds)
        print(health_care_magic_ds["train"][i])
        print("=========")
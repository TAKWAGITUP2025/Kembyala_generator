class Validators:
    @staticmethod
    def validate_numeric(value):
        """Validate that input is numeric"""
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_rib(rib_data):
        """Validate RIB has correct length (2+3+8+2)"""
        return len(rib_data) == 15
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """Validate all required fields are filled"""
        missing = [field for field in required_fields if not data.get(field)]
        return not bool(missing), missing
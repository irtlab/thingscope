
export const formatData = (data, properties) => {
    return properties.map((name) => {
        const obj = {};
        const result = [];
        data.map((val) => {
            const type = val[name]

            if (obj[type]) {
                obj[type] += 1;
            }
            else {
                obj[[type]] = 1;
            }
        });

        Object.entries(obj).forEach(([key, value]) => {
            if (key){
                result.push({
                    name: key,
                    count: value
                })
            }
            
        });

        result.sort((a, b) => (a.count < b.count) ? 1 : -1)
        return result;
    });

}
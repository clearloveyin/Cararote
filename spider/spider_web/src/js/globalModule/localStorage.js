class localStorageFun {
    constructor (name, dataName) {
        this.name = name
        this.dataName = dataName
    }
    setLocalStorage () {
        let localTime = new Date()
        let data = {
            dataName: this.dataName,
            time: localTime
        }
        localStorage.setItem(this.name, JSON.stringify(data))
    }
    getLocalStorage () {
        let localTimeNow = new Date()
        let localStorageData = JSON.parse(localStorage.getItem(this.name))
        let leadTime = localTimeNow - localStorageData.time
        let hours = Math.floor(leadTime % (24 * 3600 * 1000) / (3600 * 1000))
        if (hours >= 12) {//如果大于等于12小时则清除，否则返回data
            localStorage.removeItem(this.name)
            return null
        }
        return localStorageData.dataName
    }
}

export default localStorageFun

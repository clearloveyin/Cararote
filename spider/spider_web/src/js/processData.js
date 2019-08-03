
class processingData{
    constructor(data,projectId,userId,type) {
        this.data = data
        this.projectId = projectId
        this.userId = userId
        this.type = type
    }
    sendListData(){

    }
    sendTreeData(){

    }
    getDataType(){
        let type = Object.prototype.isPrototypeOf(this.data)

        return type
    }
    getData(data){
        
        for (let index = 0; index < data.length; index++) {
            const element = data[index];
            
        }

    }
}
class Divisao {
    constructor(divisao){
        this.divisao = [... new Set(divisao)];
    };
    
    add_item(item){
        let lista = this.divisao;
        lista.push(item);
        this.divisao = [... new Set(lista)];

    };

    remover_item(item){
        const indice = this.divisao.indexOf(item);
        if (indice !== -1){
            this.divisao.splice(indice, 1);
        }
    }

    remover_tudo(){
        this.divisao = [];
    }

}

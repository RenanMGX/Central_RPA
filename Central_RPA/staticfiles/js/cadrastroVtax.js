class Empresas {
    constructor() {
        this.empresas = {};
    };

    get_empresas() {
        return this.empresas;
    };

    add_empresa(empresa){
        if (this.empresas.length === 0){
            this.empresas[1] = empresa;
            return;
        }
        const keys = Object.keys(this.empresas);
        this.empresas[keys.length + 1] = empresa;
    }

    remover_empresa(empresa){
        const indice = this.empresas.indexOf(empresa);
        if (indice !== -1){
            this.empresas.splice(indice, 1);
        }
    }

    remover_empresa_per_id(id){
        try{
            delete this.empresas[id];
        } catch (error) {
            console.error("Erro ao remover empresa: ", error);
        }
    }

}
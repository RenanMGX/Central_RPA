class Empresas {
    static count = 0

    constructor() {
        this.empresas = {};
    };

    get_empresas() {
        return this.empresas;
    };

    add_empresa(empresa){
        if (!Object.values(this.empresas).includes(empresa)){
            this.empresas[Empresas.count] = empresa;
            Empresas.count++;
            // console.log(Empresas.count);
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
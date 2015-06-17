
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


public class DiscreteEventSimulation {

	public static void main(String[] args) {
            System.out.println("Escoja el tipo de Simulacion: ");
            System.out.println("1: Para simulacion estocastica");
            System.out.println("2: Para simulacion desde un trace driven");
            System.out.println("Ingrese su opcion: ");
            
            try{
                BufferedReader bufferRead = new BufferedReader(new InputStreamReader(System.in));
                String input = bufferRead.readLine();
                int i = Integer.parseInt(input);
                switch (i){
                    case 1 : 
                        Simulation s1 = new Simulation();
                        s1.simulation_type = 1;
                        s1.setup(); // setup simulation;
                        s1.run(10000); // run of simulation
                        break;
                    case 2: 
                        Simulation s2 = new Simulation();
                        s2.simulation_type = 2;
                        s2.createTraceDriven();
                        s2.readTrace();
                        s2.setup(); 
                        s2.run(10000); 
                        break;
                    default: 
                        System.out.println("Opciones 1 y 2. Ejecute nuevamente :(");
                }
                System.out.println("Fin de la simulacion :)");
                System.out.println("Ejecutar nuevamente para probar otra opcion");
            }catch(Exception e){
                System.out.println("Debe ingresar numeros enteros, 1 o 2 :)");
                System.out.println("Ejecutar nuevamente para probar otra opcion");
            }
	}

}

import { useNavigate } from "react-router-dom";
import styled from 'styled-components';

export default function Home() {
	const navigate = useNavigate();

	const project = () => {
		navigate("/project");
	}

	return (
		<Cont>
            <Box>
                <div class="input-group mb-3" style={{width:"100%"}}>
                    <span class="input-group-text" id="inputGroup-sizing-default">Project Name</span>
                    <input type="text" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default"/>
                </div>
                <div class="input-group mb-3" style={{width:"100%"}}>
                    <label class="input-group-text" for="inputGroupSelect01">Model</label>
                    <select class="form-select" id="inputGroupSelect01">
                        <option selected>Choose Model</option>
                        <option value="1">Chat GPT</option>
                        <option value="2">Gemini</option>
                        <option value="3">AnimeGANv2</option>
                    </select>
                </div>
                <button type="button" class="btn btn-primary" onClick={project}>Create Project</button>
            </Box>
		</Cont>
	)
}

const Cont = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100vw;
    height: 100vh;
`;

const Box = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 50vw;
    height: 30vh;
`;

const ProjectName = styled.div`
    width: 100%;
    height: 50%;
`;

const ModelName = styled.div`
    width: 100%;
    height: 50%;
`;
